import {
  PluginInitializerContext,
  CoreSetup,
  CoreStart,
  Plugin,
  Logger,
} from 'kibana/server'; // <--- Points to our mock file

import { defineRoutes } from './routes';

export class AutofixerKibanaPlugin implements Plugin<void, void> {
  private readonly logger: Logger;

  constructor(initializerContext: PluginInitializerContext) {
    this.logger = initializerContext.logger.get();
  }

  public setup(core: CoreSetup) {
    this.logger.info('🤖 Auto-Fixer Agent: Initializing...');

    const router = core.http.createRouter();

    // Register API Routes
    defineRoutes(router);

    return {};
  }

  public start(core: CoreStart) {
    this.logger.info('🤖 Auto-Fixer Agent: Started!');
    return {};
  }

  public stop() {}
}