import {
    Component,
    ElementRef,
    OnInit,
} from '@angular/core';

import { MonitoringService } from '../app/services/monitoring-api.service';
import { Monitoring } from './model/monitoring';

@Component({
    selector: 'app',
    template: require('./app.component.html'),
    // template: `
    //     <pre>{{ monitoring | json}}</pre>
    // `,
    providers: [
        MonitoringService
    ]
})
export class AppComponent implements OnInit {

    monitoring_id: number;
    organizaiton_id: number;
    mode: string;
    monitoring: Monitoring;

    constructor(
        private _el: ElementRef,
        private _montiroingSrvice: MonitoringService
    ) {
        let nativeElement = this._el.nativeElement;
        this.monitoring_id = +nativeElement.getAttribute('monitoring-id');
        this.organizaiton_id = +nativeElement.getAttribute('organizaiton-id');
        this.mode = nativeElement.getAttribute('mode') || 'editor';
    }

    ngOnInit() {
        if (this.monitoring_id > 0) {
            this._montiroingSrvice
                .getMonitoring(this.monitoring_id)
                .subscribe(
                    (m => this.monitoring = m),
                    (error => console.log(error) )
                );
        } else {
            this.monitoring = new Monitoring();
        }

    }
}
