/**
 * CSV parsing for roster import (FR-ORG-03).
 *
 * Deliberately small and deliberately dumb: it splits the file into rows and
 * maps the header names onto the fields the API expects, and does nothing else.
 * Every conversion and every rule — digits, groups, versions, duplicates — is the
 * server's, so a browser that parses the file slightly differently cannot change
 * what gets imported.
 */

import type { RawRosterRow } from "../api/roster";

const QUOTE = '"';
const COMMA = ",";

/**
 * Split RFC 4180 text into rows of cells.
 *
 * Handles quoted fields, escaped quotes (`""`), and newlines inside quotes —
 * a Bangla name with a comma in it is common enough to be worth getting right.
 */
export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;
  let index = 0;

  const endCell = (): void => {
    row.push(cell);
    cell = "";
  };
  const endRow = (): void => {
    endCell();
    rows.push(row);
    row = [];
  };

  // Strip the UTF-8 BOM Excel writes, which would otherwise become part of the
  // first header name and stop it matching.
  const source = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;

  while (index < source.length) {
    const char = source[index];

    if (quoted) {
      if (char === QUOTE) {
        if (source[index + 1] === QUOTE) {
          cell += QUOTE;
          index += 2;
          continue;
        }
        quoted = false;
        index += 1;
        continue;
      }
      cell += char;
      index += 1;
      continue;
    }

    if (char === QUOTE && cell === "") {
      quoted = true;
      index += 1;
      continue;
    }
    if (char === COMMA) {
      endCell();
      index += 1;
      continue;
    }
    if (char === "\r") {
      index += 1;
      continue;
    }
    if (char === "\n") {
      endRow();
      index += 1;
      continue;
    }
    cell += char;
    index += 1;
  }

  if (cell !== "" || row.length > 0) endRow();
  return rows.filter((cells) => cells.some((value) => value.trim() !== ""));
}

/** Header names a school might use, in either language, for each field. */
const HEADER_ALIASES: Record<keyof Omit<RawRosterRow, "row_number">, string[]> =
  {
    roll: ["roll", "roll no", "roll number", "রোল", "রোল নং"],
    student_uid: ["student id", "student uid", "id", "আইডি"],
    name_bn: ["name bn", "name (bn)", "bangla name", "নাম", "বাংলা নাম"],
    name_en: ["name en", "name (en)", "english name", "name", "ইংরেজি নাম"],
    class_level: ["class", "class level", "শ্রেণি", "ক্লাস"],
    group_code: ["group", "বিভাগ", "গ্রুপ"],
    version: ["version", "medium", "ভার্সন", "মাধ্যম"],
    shift: ["shift", "শিফট"],
    section: ["section", "শাখা"],
    fourth_subject_code: [
      "fourth subject",
      "4th subject",
      "চতুর্থ বিষয়",
      "ঐচ্ছিক বিষয়",
    ],
    guardian_mobile: [
      "guardian mobile",
      "guardian phone",
      "mobile",
      "অভিভাবকের মোবাইল",
      "মোবাইল",
    ],
  };

function normaliseHeader(value: string): string {
  return value.trim().toLowerCase().replace(/[_-]+/g, " ").replace(/\s+/g, " ");
}

/** Which column holds which field, or `null` for a column we do not use. */
export function mapHeaders(
  header: string[],
): (keyof Omit<RawRosterRow, "row_number"> | null)[] {
  const lookup = new Map<string, keyof Omit<RawRosterRow, "row_number">>();
  for (const [field, aliases] of Object.entries(HEADER_ALIASES)) {
    for (const alias of aliases) {
      // First alias wins, so "name" stays English when "name en" is absent.
      if (!lookup.has(alias)) {
        lookup.set(alias, field as keyof Omit<RawRosterRow, "row_number">);
      }
    }
  }
  return header.map((cell) => lookup.get(normaliseHeader(cell)) ?? null);
}

export interface ParsedRoster {
  rows: RawRosterRow[];
  /** Header cells that matched no known field; shown so the admin can rename them. */
  unknownColumns: string[];
  /** True when the header carried no recognisable column at all. */
  headerUnrecognised: boolean;
}

/**
 * Turn CSV text into rows the API accepts.
 *
 * `row_number` counts data rows from 1 and is what every reported problem refers
 * back to, so it has to match what the admin sees in their spreadsheet.
 */
export function parseRosterCsv(text: string): ParsedRoster {
  const table = parseCsv(text);
  if (table.length === 0) {
    return { rows: [], unknownColumns: [], headerUnrecognised: true };
  }

  const [header = [], ...body] = table;
  const fields = mapHeaders(header);
  const unknownColumns = header.filter(
    (cell, index) => fields[index] === null && cell.trim() !== "",
  );

  const rows = body.map((cells, offset) => {
    const row: RawRosterRow = { row_number: offset + 1 };
    fields.forEach((field, index) => {
      if (field === null) return;
      row[field] = (cells[index] ?? "").trim();
    });
    return row;
  });

  return {
    rows,
    unknownColumns,
    headerUnrecognised: fields.every((field) => field === null),
  };
}
