import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule} from './App.module';
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
import { LoggerService } from './services/Logger';
import { LogRequestInterceptor} from './interceptors/LogRequest.interceptor';
import { AccessGuard } from './guards/access.guards';
import fastifyCsrf from 'fastify-csrf';
import * as csurf from 'csurf';

async function bootstrap() {
    const app = await NestFactory.create<NestFastifyApplication>(
        AppModule,
        new FastifyAdapter()
    );

    app.register(fastifyCsrf);
    app.useLogger(app.get(LoggerService));
    app.useGlobalGuards(app.get(AccessGuard))
    app.useGlobalInterceptors(app.get(LogRequestInterceptor));

    // @TODO: load plugins interceptors

    // Pipes
    app.useGlobalPipes(new ValidationPipe({
        whitelist:true
    }));

    await app.listen(3000);
}

bootstrap().catch(e => {
    console.log("Cannot bootstrap API");
    console.log(e);
});
