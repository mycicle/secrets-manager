import { Document } from 'mongoose';

export interface SecretDB extends Document {
    app_name: string,
    app_password?: string,
    mnemonic?: string[],
    pin?: number[],
    additional?: string,
}

export default SecretDB;