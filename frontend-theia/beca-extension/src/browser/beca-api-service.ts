import { injectable } from 'inversify';
import axios, { AxiosInstance } from 'axios';

export interface BECAMessage {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

export interface BECAResponse {
    response: string;
    files_modified?: string[];
    error?: string;
}

export interface BECAStatus {
    status: string;
    model?: string;
    mode?: string;
    error?: string;
}

@injectable()
export class BECAApiService {
    private apiClient: AxiosInstance;
    private apiUrl: string;

    constructor() {
        // Dynamically determine API URL based on current host
        // This allows the frontend to work with any external IP
        const protocol = window.location.protocol; // http: or https:
        const hostname = window.location.hostname; // e.g., 34.134.149.22 or localhost
        
        // If BECA_API_URL is explicitly set in environment, use it
        // Otherwise, use the same host as frontend but port 8000
        this.apiUrl = process.env.BECA_API_URL || `${protocol}//${hostname}:8000`;
        
        console.log(`BECA API URL: ${this.apiUrl}`);
        
        this.apiClient = axios.create({
            baseURL: this.apiUrl,
            timeout: 300000, // 5 minutes for long-running tasks
            headers: {
                'Content-Type': 'application/json',
            }
        });
    }
    setApiUrl(url: string): void {
        this.apiUrl = url;
        console.log(`BECA API URL updated to: ${this.apiUrl}`);
        this.apiClient = axios.create({
            baseURL: this.apiUrl,
            timeout: 300000,
            headers: {
                'Content-Type': 'application/json',
            }
        });
    }

    /**
     * Send a message to BECA and get a response
     */
    async sendMessage(message: string, mode: 'plan' | 'act' = 'act'): Promise<BECAResponse> {
        try {
            const response = await this.apiClient.post('/chat', {
                message,
                mode,
                stream: false
            });
            return response.data;
        } catch (error: any) {
            console.error('Error sending message to BECA:', error);
            return {
                response: `Error: ${error.response?.data?.detail || error.message}`,
                error: error.message
            };
        }
    }

    /**
     * Get BECA's current status
     */
    async getStatus(): Promise<BECAStatus> {
        try {
            const response = await this.apiClient.get('/status');
            return response.data;
        } catch (error: any) {
            console.error('Error getting BECA status:', error);
            return {
                status: 'error',
                error: error.message
            };
        }
    }

    /**
     * Get chat history
     */
    async getChatHistory(): Promise<BECAMessage[]> {
        try {
            const response = await this.apiClient.get('/chat/history');
            return response.data.history || [];
        } catch (error: any) {
            console.error('Error getting chat history:', error);
            return [];
        }
    }

    /**
     * Clear chat history
     */
    async clearHistory(): Promise<void> {
        try {
            await this.apiClient.post('/chat/clear');
        } catch (error: any) {
            console.error('Error clearing chat history:', error);
        }
    }

    /**
     * List files in a directory
     */
    async listFiles(path: string, recursive: boolean = false): Promise<string[]> {
        try {
            const response = await this.apiClient.post('/files/list', {
                path,
                recursive
            });
            return response.data.files || [];
        } catch (error: any) {
            console.error('Error listing files:', error);
            return [];
        }
    }

    /**
     * Read file contents
     */
    async readFile(path: string): Promise<string> {
        try {
            const response = await this.apiClient.post('/files/read', { path });
            return response.data.content || '';
        } catch (error: any) {
            console.error('Error reading file:', error);
            throw error;
        }
    }

    /**
     * Write file contents
     */
    async writeFile(path: string, content: string): Promise<void> {
        try {
            await this.apiClient.post('/files/write', { path, content });
        } catch (error: any) {
            console.error('Error writing file:', error);
            throw error;
        }
    }

    /**
     * Get current API URL
     */
    getApiUrl(): string {
        return this.apiUrl;
    }
}
