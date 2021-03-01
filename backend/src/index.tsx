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
