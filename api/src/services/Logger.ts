import { ConsoleLogger, Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class LoggerService extends ConsoleLogger {
    error(message: any, stack?: string, context?: string) {
        axios.post("https://hooks.slack.com/services/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", {"text": `Error on platform: ${message}`})
        super.error.apply(this, arguments);
    }
}