import {QuestionBase} from './question-base';

export class LongTextQuestion extends QuestionBase<string> {
    controlType = 'long_text';
    inputType: string;

    constructor(options: {} = {}) {
        super(options);
    }
}
