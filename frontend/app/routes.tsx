// import { type RouteConfig, index } from "@react-router/dev/routes";
//
// export default [index("routes/login.tsx")] satisfies RouteConfig;
import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/login.tsx"),
  route("/upload", "routes/upload.tsx"),
  route("/tester", "routes/tester.tsx"),
  route("/history", "routes/predictionHistory.tsx")
] satisfies RouteConfig;
