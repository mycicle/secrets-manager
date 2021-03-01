import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";
import express, { Express } from "express";
import cors from "cors";
import connectMongo from './connectdb';
import secretRoutes from './routes';

const app: Express = express();

const PORT: string | number = process.env["PORT"] || 4000;

app.use(cors());
app.use(secretRoutes);

connectMongo(() => 
    app.listen(PORT, () => 
        console.log(`Server running on http://localhost:${PORT}`)
    )
);

const Content = () => (
  <h1>My React and TypeScript App! {" "}
  {new Date().toLocaleDateString()}</h1>
);

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Content />
    </Router>
  </React.StrictMode>,

  document.getElementById("root")
);