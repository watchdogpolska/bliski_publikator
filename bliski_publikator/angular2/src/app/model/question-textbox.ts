import {QuestionBase} from './question-base';

export class TextboxQuestion extends QuestionBase<string>{
    controlType = 'short_text';
    inputType: string;

    constructor(options: {} = {}) {
        super(options);
        this.inputType = options['inputType'] || 'text';
    }

    toPlainObject(questions:QuestionBase<any>[]){
        let obj = super.toPlainObject(questions);
        obj['inputType'] = this.inputType;
        return obj;
    }
}
