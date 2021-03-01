import { Router } from 'express';
import { getSecrets, addSecret, updateSecret, deleteSecret } from '../controllers/secrets';

const router: Router = Router();

router.get("/secrets", getSecrets);

router.post("/add-secret", addSecret);

router.put("/update-secret/:id", updateSecret);

router.delete("/delete-secret/:id", deleteSecret);

export default router;