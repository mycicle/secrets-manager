import axios, { AxiosResponse, AxiosStatic } from 'axios';

const baseUrl: string = "http://localhost:4000";

export const getSecrets = async (): Promise<AxiosResponse<ApiDataType>> => {
    try {
        const secrets: AxiosResponse<ApiDataType> = await axios.get(
            baseUrl + "/secrets"
        )
        return secrets;
    } catch(error) {
        throw new Error(error);
    }
}

export const addSecret = async (
    formData: SecretDB
): Promise<AxiosResponse<ApiDataType>> => {
    try {
        const secret: Omit<SecretDB, "_id"> = {
            app_name: formData.app_name,
            app_password: formData.app_password,
            mnemonic: formData.mnemonic,
            pin: formData.pin,
            additional: formData.additional,
        };

        const saveSecret: AxiosResponse<ApiDataType> = await axios.post(
            baseUrl + "/add-secret",
            secret
        );

        return saveSecret;
    } catch (error) {
        throw new Error(error);
    }
}

export const updateSecret = async (
    orig_secret_id: string,
    new_secret: SecretDB,
): Promise<AxiosResponse<ApiDataType>> => {
    try {
        const updatedSecret: AxiosResponse<ApiDataType> = await axios.put(
            `${baseUrl}/update-secret/${orig_secret_id}`,
            new_secret,
        );

        return updatedSecret;
    } catch (error) {
        throw new Error(error);
    }
}

export const deleteSecret = async (
    _id: string,
): Promise<AxiosResponse<ApiDataType>> => {
    try {
        const deletedSecret: AxiosResponse<ApiDataType> = await axios.delete(
            `${baseUrl}/delete-secret/${_id}`,
        );

        return deletedSecret;
    } catch (error) {
        throw new Error(error);
    }
}