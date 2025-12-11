// import { type RouteConfig, index } from "@react-router/dev/routes";
//
// export default [index("routes/login.tsx")] satisfies RouteConfig;
import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/login.tsx"),        // "/" → login
  route("/upload", "routes/upload.tsx"), // "/upload" → upload page
] satisfies RouteConfig;
