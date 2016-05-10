import {Component, Input} from '@angular/core'
import {QuestionBase} from '../model/question-base'

@Component({
    selector: 'sowp-question-view',
    template: require('./question-view.component.html'),
    styles: [`
        sowp-question-view{
            border: 8px solid #DDD
        }`]
})
export class QuestionViewComponent{

    @Input('question')
    question: QuestionBase<any>

    constructor(){

    }
}
