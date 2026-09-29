import { describe, expect, test } from "vitest";
import { mapHeaders, parseCsv, parseRosterCsv } from "./csv";

describe("parseCsv", () => {
  test("splits plain rows and cells", () => {
    expect(parseCsv("a,b\n1,2\n")).toEqual([
      ["a", "b"],
      ["1", "2"],
    ]);
  });

  test("keeps a comma inside a quoted cell", () => {
    expect(parseCsv('name,roll\n"Uddin, Rahim",101')).toEqual([
      ["name", "roll"],
      ["Uddin, Rahim", "101"],
    ]);
  });

  test("unescapes a doubled quote", () => {
    expect(parseCsv('a\n"say ""hi"""')).toEqual([["a"], ['say "hi"']]);
  });

  test("keeps a newline inside a quoted cell", () => {
    expect(parseCsv('a,b\n"one\ntwo",3')).toEqual([
      ["a", "b"],
      ["one\ntwo", "3"],
    ]);
  });

  test("handles CRLF line endings", () => {
    expect(parseCsv("a,b\r\n1,2\r\n")).toEqual([
      ["a", "b"],
      ["1", "2"],
    ]);
  });

  test("drops the byte order mark Excel writes", () => {
    expect(parseCsv("﻿roll,name\n101,Rahim")[0]?.[0]).toBe("roll");
  });

  test("skips entirely blank rows", () => {
    expect(parseCsv("a\n\n\nb")).toEqual([["a"], ["b"]]);
  });

  test("returns nothing for an empty file", () => {
    expect(parseCsv("")).toEqual([]);
  });
});

describe("mapHeaders", () => {
  test("recognises English headers however they are spaced or cased", () => {
    expect(mapHeaders(["Roll No", "CLASS_LEVEL", " Section "])).toEqual([
      "roll",
      "class_level",
      "section",
    ]);
  });

  test("recognises Bangla headers", () => {
    expect(mapHeaders(["রোল", "শ্রেণি", "শাখা", "বিভাগ"])).toEqual([
      "roll",
      "class_level",
      "section",
      "group_code",
    ]);
  });

  test("reports an unknown column as null rather than guessing", () => {
    expect(mapHeaders(["roll", "blood group"])).toEqual(["roll", null]);
  });
});

describe("parseRosterCsv", () => {
  const FILE = [
    "Roll,Name (BN),Name (EN),Class,Group,Version,Shift,Section",
    "101,রহিম উদ্দিন,Rahim Uddin,9,Science,BM,Day,A",
    "102,করিম মিয়া,Karim Mia,9,Science,BM,Day,A",
  ].join("\n");

  test("numbers data rows from one, not counting the header", () => {
    expect(parseRosterCsv(FILE).rows.map((r) => r.row_number)).toEqual([1, 2]);
  });

  test("maps each column onto the field the API expects", () => {
    expect(parseRosterCsv(FILE).rows[0]).toEqual({
      row_number: 1,
      roll: "101",
      name_bn: "রহিম উদ্দিন",
      name_en: "Rahim Uddin",
      class_level: "9",
      group_code: "Science",
      version: "BM",
      shift: "Day",
      section: "A",
    });
  });

  test("passes values through untouched for the server to validate", () => {
    const parsed = parseRosterCsv("Roll,Class,Section\n১০১,৯,ক");
    expect(parsed.rows[0]?.roll).toBe("১০১");
  });

  test("names the columns it did not recognise", () => {
    const parsed = parseRosterCsv("Roll,Blood Group\n101,B+");
    expect(parsed.unknownColumns).toEqual(["Blood Group"]);
    expect(parsed.headerUnrecognised).toBe(false);
  });

  test("flags a header with nothing recognisable in it", () => {
    expect(parseRosterCsv("x,y\n1,2").headerUnrecognised).toBe(true);
  });

  test("flags an empty file", () => {
    expect(parseRosterCsv("")).toEqual({
      rows: [],
      unknownColumns: [],
      headerUnrecognised: true,
    });
  });

  test("a header with no data rows yields no rows", () => {
    expect(parseRosterCsv("Roll,Class,Section").rows).toEqual([]);
  });
});
