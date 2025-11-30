import { supabase } from "./supabase";

export async function insertMotionLog() {
  return await supabase.from("motion_logs").insert({});
}

export async function getMotionCount(hours: number = 1) {
  const hoursAgo = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();

  const { count } = await supabase
    .from("motion_logs")
    .select("*", { count: "exact", head: true })
    .gte("timestamp", hoursAgo);

  return count || 0;
}

export async function insertGasLog(value: number) {
  return await supabase.from("gas_logs").insert({ value });
}

export async function getGasCount() {
  const { count } = await supabase
    .from("gas_logs")
    .select("*", { count: "exact", head: true });

  return count || 0;
}

export async function insertTemperatureLog(temp: number, humidity: number) {
  return await supabase.from("temperature_logs").insert({
    temp,
    humidity,
  });
}

export async function getLatestTemperature() {
  const { data } = await supabase
    .from("temperature_logs")
    .select("temp, timestamp")
    .order("timestamp", { ascending: false })
    .limit(1);

  return data && data.length > 0 ? data[0] : null;
}

export async function getLatestHumidity() {
  const { data } = await supabase
    .from("temperature_logs")
    .select("humidity, timestamp")
    .order("timestamp", { ascending: false })
    .limit(1);

  return data && data.length > 0 ? data[0] : null;
}

export async function getUserByRfidCard(cardId: string) {
  const { data } = await supabase
    .from("users")
    .select("id, name")
    .eq("rfid_card", cardId)
    .single();

  return data;
}

export async function insertRfidScan(
  cardId: string,
  success: boolean,
  userId: number | null = null
) {
  return await supabase.from("rfid_scans").insert({
    card_id: cardId,
    success,
    user_id: userId,
    timestamp: new Date().toISOString(),
  });
}

export async function getRfidScans(limit: number = 100) {
  const { data, error } = await supabase
    .from("rfid_scans")
    .select(
      `
      id,
      card_id,
      success,
      user_id,
      timestamp,
      users (
        name
      )
    `
    )
    .order("timestamp", { ascending: false })
    .limit(limit);

  if (error) {
    console.error("Error fetching RFID scans:", error);
    return [];
  }

  return data || [];
}
