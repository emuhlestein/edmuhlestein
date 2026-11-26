export function isLoggedIn(req) {
  return !!req.session.userId;
}