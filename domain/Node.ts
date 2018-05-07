export class Node {
    temperature: number;
    light: number;
    time: number;
    id: string;

    constructor(temperature: number, light: number, time: number, id: string) {
        this.temperature = temperature;
        this.light = light;
        this.time = time;
        this.id = id;
    }
}