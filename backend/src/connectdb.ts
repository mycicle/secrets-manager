import mongoose from 'mongoose';

export default async (callback: CallableFunction): Promise<void> => {
    const mongoConnectString: string | undefined = process.env["MONGO_URI"];

    if (!mongoConnectString) {
        console.log('Error, cannot load MONGO_URI from environment');
    }
    mongoose.connect(mongoConnectString ? mongoConnectString : "", await callback());
}
