// settings.js
function required(name) {
  const value = process.env[name];
  if (!value) throw new Error(`missing ${name}`);
  return value;
}

export const settings = {
  port: Number(process.env.PORT || 3000),
  databaseUrl: required("DATABASE_URL"),
};