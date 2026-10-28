function required(name) {
  const value = process.env[name];
  if (value === undefined || value === "") {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export const settings = {
  databaseUrl: required("DATABASE_URL"),
  debug: process.env.DEBUG === "True" || process.env.DEBUG === "true",
  secretKey: required("SECRET_KEY"),
  jwtSecret: required("JWT_SECRET"),
  algorithm: process.env.ALGORITHM || "HS256",
  accessTokenExpireMinutes: Number(process.env.ACCESS_TOKEN_EXPIRE_MINUTES) || 15,
  refreshTokenExpireDays: Number(process.env.REFRESH_TOKEN_EXPIRE_DAYS) || 5,
};