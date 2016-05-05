import { Serializable } from '../serializable';
import { QuestionBase } from '../model/question-base';


export abstract class BaseConditional {
    type: string;
    constructor(options: {
        type?:string,
    }){
        this.type = options['type'] || '';
    }

    abstract isValid(answers):boolean;

    toPlainObject(questions: QuestionBase<any>[]) {
        let obj = {};
        obj[ 'type' ] = this.type;
        return obj;
    }
}
