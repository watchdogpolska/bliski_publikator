import { Serializable } from '../serializable';

export abstract class BaseConditional implements Serializable {
    type: string;
    constructor(options: {
        type?:string,
    }){
        this.type = options['type'] || '';
    }
    
    abstract isValid(answers):boolean;
    toPlainObject(){
        let obj = {};
        obj[ 'type' ] = this.type;
        return obj;
    }
}
