import { injectable } from 'inversify';
import { AbstractViewContribution } from '@theia/core/lib/browser';
import { BECAChatWidget } from './beca-chat-widget';
import { Command, CommandRegistry, MenuModelRegistry } from '@theia/core/lib/common';

export const BECAChatCommand: Command = {
    id: 'beca-chat:toggle',
    label: 'Toggle BECA Chat'
};

@injectable()
export class BECAViewContribution extends AbstractViewContribution<BECAChatWidget> {
    constructor() {
        super({
            widgetId: BECAChatWidget.ID,
            widgetName: BECAChatWidget.LABEL,
            defaultWidgetOptions: {
                area: 'right',
                rank: 500
            },
            toggleCommandId: BECAChatCommand.id
        });
    }

    registerCommands(commands: CommandRegistry): void {
        commands.registerCommand(BECAChatCommand, {
            execute: () => super.openView({ activate: true, reveal: true })
        });
    }

    registerMenus(menus: MenuModelRegistry): void {
        super.registerMenus(menus);
    }
}
