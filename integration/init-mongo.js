db.createUser(
    {
        user: "macau",
        pwd: "macau",
        roles: [
            {
                role: "readWrite",
                db: "structuralcity"
            }
        ]
    }
)