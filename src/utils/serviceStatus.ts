enum ServiceKey {
  Score = "score",
  Schedule = "schedule",
}

// 10分钟轮询间隔
const UPDATE_INTERVAL = 10 * 60 * 1000;

interface ServiceStatusResponse {
  lastUpdated: number;
  items: ServiceStatusItems;
}

const EMPTY_SERVICE_STATUS: ServiceStatusResponse = {
  lastUpdated: 0,
  items: {}
}

type ServiceStatusItems = {
  [key in ServiceKey]?: ServiceStatusData;
};

interface ServiceStatusData {
  type: "info" | "warning" | "error";
  message: string;
}

export type {
  ServiceStatusResponse,
  ServiceStatusItems,
  ServiceStatusData,
}

export { ServiceKey, UPDATE_INTERVAL, EMPTY_SERVICE_STATUS };
