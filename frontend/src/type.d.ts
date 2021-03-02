interface SecretDB {
    _id: string
    app_name: string,
    app_password?: string,
    mnemonic?: string[],
    pin?: number[],
    additional?: string,
    createdAt?: string,
    updatedAt?: string,
}

interface SecretProps {
    secret: SecretDB,
}

type ApiDataType = {
    message: string,
    status: string,
    secret?: SecretDB,
    secrets: SecretDB[],
}