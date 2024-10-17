import http from "./http"; // Assuming this is an Axios instance

const testresultshow = (params) => {
  const path = "/home/testresult";
  return http.get(path); // Make a GET request to the backend
};
// const testQ1 = () => {
//   const path = "/home/chartq1";
//   return http.get(path); // Make a GET request to the backend
// };
// Axios API call
// const testQ1 = (params) => {
//   const path = "/home/chartq1";
//   return http.Uploadfigure(path, {  responseType: "blob" }); // Set responseType to 'blob'
// };

// const testGain = (params) => {
//   const path = "/home/chartgain";
//   return http.Uploadfigure(path, { params, responseType: "blob" }); // Set responseType to 'blob'
// };
const testQ1 = (params) => {
  const path = "/home/chartq1";
  return http.Uploadfigure(path, params); // Pass params directly
};

const testGain = (params) => {
  const path = "/home/chartgain";
  return http.Uploadfigure(path, params); // Pass params directly
};
export default {
  testresultshow,
  testQ1,
  testGain,
};
