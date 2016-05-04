
export abstract class BaseCountCondition {
    type: string;
    point: number;
    constructor(options: {
        type?: string,
        point?: number
    }) {
        this.type = options['type'] || '';
        this.point = +(options['point'] || 1);
    }

    abstract isValid(answer): boolean;

    toPlainObject() {
        let obj = {};
        obj['type'] = this.type;
        obj['point'] = this.point;
        return obj;
    }
}
