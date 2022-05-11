export function pointToPercent(point: number | string): number {
    point = Number(point)
    return (point + 9) * 100 / 18
}