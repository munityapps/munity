import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from "@nestjs/common";
import { Observable, tap } from "rxjs";

@Injectable()
export class LogRequestInterceptor implements NestInterceptor {
    intercept(context: ExecutionContext, next: CallHandler): Observable<any> {

    const now = Date.now();
    return next
        .handle()
        .pipe(
            tap(() => console.log(`After... ${Date.now() - now}ms`)),
        );
  }
}