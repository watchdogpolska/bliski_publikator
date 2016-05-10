import {Component, Input} from '@angular/core'
import {Monitoring} from '../model/monitoring'
import {QuestionViewComponent} from './question-view.component'

@Component({
    selector: 'sowp-question-viewer',
    template: require('./question-viewer.component.html'),
    directives: [
        QuestionViewComponent
    ]
})
export class QuestionViewerComponent{

    @Input()
    monitoring:Monitoring

    constructor(){

    }
}
