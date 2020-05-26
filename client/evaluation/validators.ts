export function required(value: any) : boolean {
  return !!value;
}

export function decimal(value: any) : boolean {
  return /^\d+(,\d+)?$/.test(value);
}