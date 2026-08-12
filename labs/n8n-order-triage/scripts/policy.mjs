export function triageOrder(order) {
  const validationErrors = [];
  const totalCents = Number(order?.totalCents);
  const riskScore = order?.riskScore === undefined ? 0 : Number(order.riskScore);

  if (typeof order?.orderId !== "string" || order.orderId.trim() === "") {
    validationErrors.push("orderId must be a non-empty string");
  }
  if (typeof order?.customerId !== "string" || order.customerId.trim() === "") {
    validationErrors.push("customerId must be a non-empty string");
  }
  if (typeof order?.currency !== "string" || !/^[A-Z]{3}$/.test(order.currency)) {
    validationErrors.push("currency must be a three-letter uppercase code");
  }
  if (!Number.isSafeInteger(totalCents) || totalCents < 0) {
    validationErrors.push("totalCents must be a non-negative safe integer");
  }
  if (!Number.isInteger(riskScore) || riskScore < 0 || riskScore > 100) {
    validationErrors.push("riskScore must be an integer from 0 through 100");
  }

  let route = "automatic";
  if (validationErrors.length > 0) route = "invalid";
  else if (totalCents >= 100_000 || riskScore >= 70) route = "manual_review";

  return {
    orderId: typeof order?.orderId === "string" ? order.orderId : null,
    customerId: typeof order?.customerId === "string" ? order.customerId : null,
    currency: typeof order?.currency === "string" ? order.currency : null,
    totalCents,
    riskScore,
    route,
    validationErrors,
  };
}
