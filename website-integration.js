// Add to your existing EduLIS HTML JavaScript.
// Fetch this JSON alongside your existing opportunities.json.
// Merge BEFORE your existing category filtering and sorting functions.

const MANUAL_JSON_URL =
  "https://raw.githubusercontent.com/edulispoint/edulis-lis-notification-links/main/docs/manual_notifications.json";

async function fetchManualNotifications() {
  try {
    const response = await fetch(MANUAL_JSON_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.warn("EduLIS manual notifications unavailable:", error);
    return [];
  }
}

function mergeEduLISNotifications(automaticRecords, manualRecords) {
  const seen = new Set();
  return [...(automaticRecords || []), ...(manualRecords || [])].filter(item => {
    const url = (item.official_url || "").trim().replace(/\/+$/, "").toLowerCase();
    const fallback = `${(item.post_name || "").trim().toLowerCase()}|${(item.organization || "").trim().toLowerCase()}`;
    const key = url || fallback;
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/*
Example inside your existing data-loading function:

const [autoResponse, manualRecords] = await Promise.all([
  fetch(EXISTING_OPPORTUNITIES_JSON_URL),
  fetchManualNotifications()
]);
const automaticRecords = await autoResponse.json();
const allRecords = mergeEduLISNotifications(automaticRecords, manualRecords);

// Pass allRecords to your current filtering, sorting and rendering code.
*/
