import {QuestionBase} from './question-base';

export class TextboxQuestion extends QuestionBase<string>{
    controlType = 'textbox';
    inputType: string;

    constructor(options: {} = {}) {
        super(options);
        this.inputType = options['inputType'] || 'text';
    }

    toPlainObject(){
        let obj = super.toPlainObject();
        obj['inputType'] = this.inputType;
        return obj;
    }
}
