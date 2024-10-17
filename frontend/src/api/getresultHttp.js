import http from "./http";

const getresult = (page = 1, size = 8, params) => {
  // const path = "/apps/cb22/cb22/?page=" + page;
  // const path = `/apps/cb22?page=${page}&size=${size}`;
  // return http.get(path);
  const path = "/cb22/cb22";
  params = params ? params : {};
  params["page"] = page;
  params["size"] = size;
  return http.get(path, params);
};
const downloaddata = (pks) => {
  const path = "/cb22/download";
  return http.downloadFile(path, { pks: JSON.stringify(pks) });
};
export default {
  getresult,
  downloaddata,
};
