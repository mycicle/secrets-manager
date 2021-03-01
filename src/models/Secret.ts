import SecretDB from '../types/SecretDB';
import { model, Schema } from "mongoose";

const SecretSchema: Schema = new Schema(
    {
        app_name: {
            type: String,
            required: true,
        },
        app_password: {
            type: String,
            required: false,
        },
        mnemonic: {
            type: [String],
            required: false,
        },
        pin: {
            type: [Number],
            required: false,
        },
        additional: {
            type: String,
            required: false,
        },
    },
    { timestamps: true },
);

export default model<SecretDB>("Secret", SecretSchema);