// import { useRoutes } from "react-router-dom";
// import { routes } from "./react-router.config";
//
// function App() {
//   const routing = useRoutes(
//     routes.map(route => ({
//       path: route.path,
//       element: <route.Component />,
//     }))
//   );
//   return routing;
// }
//
// export default App;

import React from "react";
import { useRoutes } from "react-router-dom";
import routes from "../react-router.config";

export default function App() {
  const routing = useRoutes(routes);
  return <>{routing}</>;
}
