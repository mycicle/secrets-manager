import { Response, Request } from "express";
import SecretDB from "../../types/SecretDB";
import Secret from "../../models/Secret";

export const getSecrets = async (req: Request, res: Response): Promise<void> => {
    try {
        const secrets: SecretDB[] = await Secret.find();
        res.status(200).json({ secrets });
    } catch (error) {
        throw error;
    }
}

export const addSecret = async (req: Request, res: Response): Promise<void> => {
    try {
        const body = req.body as 
            Pick<SecretDB, "app_name" | "app_password" | "mnemonic" | "pin" | "additional">;
        
        const secret: SecretDB = new Secret({
            app_name: body.app_name,
            app_password: body.app_password,
            mnemonic: body.mnemonic,
            pin: body.pin,
            additional: body.additional,
        });

        const newSecret: SecretDB = await secret.save();
        const allSecrets: SecretDB[] = await Secret.find();

        res
            .status(201)
            .json({
                message: "Secret added",
                secret: newSecret,
                secrets: allSecrets,
            });
    } catch (error) {
        throw error;
    }
}

export const updateSecret = async (req: Request, res: Response): Promise<void> => {
    try {
        const {
            params: { id },
            body,
        } = req;
        const updateSecret: SecretDB | null = await Secret.findByIdAndUpdate(
            { _id: id },
            body,
        );
        const allSecrets: SecretDB[] = await Secret.find();
        res
            .status(200)
            .json({
                message: "Secret updated",
                secret: updateSecret,
                secrets: allSecrets,
            });
    } catch (error) {
        throw error;
    }
}

export const deleteSecret = async (req: Request, res: Response): Promise<void> => {
    try {
        const deletedSecret: SecretDB | null = await Secret.findByIdAndRemove(
            req.params.id,
        );
        const allSecrets: SecretDB[] = await Secret.find();
        res
            .status(200)
            .json({
                message: "Secret deleted",
                secret: deletedSecret,
                secrets: allSecrets,
            });
    } catch (error) {
        throw error;
    }
}