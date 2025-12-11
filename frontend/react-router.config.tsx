import Login from "./app/routes/login";
import Upload from "./app/routes/upload";

const routes = [
  { path: "/", element: <Login /> },
  { path: "/upload", element: <Upload /> },
];

export default routes;
