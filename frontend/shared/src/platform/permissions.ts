/** Client-side permission matcher aligned with backend PermissionEvaluator. */

export function matchesPermission(
  userPermissions: readonly string[],
  required: string,
): boolean {
  if (userPermissions.includes("*")) return true;
  return userPermissions.includes(required);
}

export function matchesAnyPermission(
  userPermissions: readonly string[],
  required: string | readonly string[] | undefined,
): boolean {
  if (!required) return true;
  const codes = typeof required === "string" ? [required] : required;
  if (codes.length === 0) return true;
  return codes.some((code) => matchesPermission(userPermissions, code));
}
