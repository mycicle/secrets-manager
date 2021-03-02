import React from "react";

type Props = SecretProps & {
    updateSecret: (secret: SecretDB) => void,
    deleteSecret: (_id: string) => void,
}

const Secret: React.FC<Props> = ({ secret, updateSecret, deleteSecret }) => {
    const checkSecret: string = secret.
}