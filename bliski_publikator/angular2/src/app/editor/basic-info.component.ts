import {
    Component,
    Input
 } from '@angular/core';

import { Monitoring } from '../model/monitoring';

@Component({
    selector: 'sowp-basic-info',
    template: require('./basic-info.component.html'),
})
export class BasicInfoComponent {
    @Input()
    monitoring: Monitoring;

}
