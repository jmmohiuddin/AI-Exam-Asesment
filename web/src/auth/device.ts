import { readStorage, removeStorage, writeStorage } from "../lib/storage";

/** device_id is a non-secret identifier that lets a known device skip OTP. */
export const DEVICE_ID_KEY = "khata.device_id";
const DEVICE_ID_RE = /^[A-Za-z0-9_-]{8,128}$/;

export function getDeviceId(): string | undefined {
  const value = readStorage(DEVICE_ID_KEY);
  return value && DEVICE_ID_RE.test(value) ? value : undefined;
}

export function saveDeviceId(deviceId: string): void {
  if (DEVICE_ID_RE.test(deviceId)) writeStorage(DEVICE_ID_KEY, deviceId);
}

export function forgetDeviceId(): void {
  removeStorage(DEVICE_ID_KEY);
}

const BROWSERS: [RegExp, string][] = [
  [/Edg\//, "Edge"],
  [/OPR\//, "Opera"],
  [/SamsungBrowser\//, "Samsung Internet"],
  [/Firefox\//, "Firefox"],
  [/Chrome\//, "Chrome"],
  [/Safari\//, "Safari"],
];

const SYSTEMS: [RegExp, string][] = [
  [/Android/, "Android"],
  [/iPhone|iPad/, "iOS"],
  [/Windows/, "Windows"],
  [/Mac OS X/, "macOS"],
  [/Linux/, "Linux"],
];

/** A human label for the device list, e.g. "Chrome on Android". */
export function describeDevice(userAgent: string): string {
  const browser = BROWSERS.find(([re]) => re.test(userAgent))?.[1] ?? "Browser";
  const system = SYSTEMS.find(([re]) => re.test(userAgent))?.[1];
  return system ? `${browser} on ${system}` : browser;
}
