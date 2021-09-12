import { HttpModule } from '@nestjs/axios';
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { AccessGuard } from './guards/access.guards';
import { LogRequestInterceptor } from './interceptors/LogRequest.interceptor';
import { LoggerService } from './services/Logger';
import { UserModule } from './modules/user/user.module';
import { GroupModule } from './modules/group/group.module';

// @TODO: Lazy load modules plugins
@Module({
    imports: [ HttpModule, UserModule, GroupModule],
    providers: [LoggerService, LogRequestInterceptor, AccessGuard],
    exports: [LoggerService],
})
export class AppModule{};
// export class AppModule implements NestModule{
//     async configure(consumer: MiddlewareConsumer) {
//         await consumer
//             .apply(LoggerMiddleware)
//             // .apply(MaintenanceMiddleware, LoggerMiddleware)
//             .forRoutes(ExampleController);
//     }
// };
