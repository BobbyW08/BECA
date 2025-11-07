import { ContainerModule } from 'inversify';
import { BECAApiService } from './beca-api-service';
import { BECAChatWidget } from './beca-chat-widget';
import { WidgetFactory } from '@theia/core/lib/browser';
import { bindViewContribution, FrontendApplicationContribution } from '@theia/core/lib/browser';
import { BECAViewContribution } from './beca-view-contribution';
import './style/beca-chat.css';

export default new ContainerModule(bind => {
    // Bind API service as singleton
    bind(BECAApiService).toSelf().inSingletonScope();

    // Bind view contribution
    bindViewContribution(bind, BECAViewContribution);
    bind(FrontendApplicationContribution).toService(BECAViewContribution);

    // Bind widget
    bind(BECAChatWidget).toSelf();
    bind(WidgetFactory).toDynamicValue(ctx => ({
        id: BECAChatWidget.ID,
        createWidget: () => ctx.container.get<BECAChatWidget>(BECAChatWidget)
    })).inSingletonScope();
});
