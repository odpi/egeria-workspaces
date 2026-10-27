/**
 * In-memory implementations of TaskStore and TaskMessageQueue.
 * WARNING: These APIs are experimental and may change without notice.
 *
 * @experimental
 */
import { Task, RequestId, Result, Request } from '../../../types.js';
import { TaskStore, TaskMessageQueue, QueuedMessage, CreateTaskOptions } from '../interfaces.js';
/**
 * A simple in-memory implementation of TaskStore for demonstration purposes.
 *
 * This implementation stores all tasks in memory and provides automatic cleanup
 * based on the ttl duration specified in the task creation parameters.
 *
 * A task created with a sessionId belongs to that session: calls that pass a different
 * sessionId treat the task as not found, and listTasks with a sessionId returns that
 * session's tasks and the tasks created without a sessionId. Calls that pass no sessionId
 * are not restricted.
 *
 * Note: This is not suitable for production use as all data is lost on restart.
 * For production, consider implementing TaskStore with a database or distributed cache.
 *
 * @experimental
 */
export declare class InMemoryTaskStore implements TaskStore {
    private tasks;
    private cleanupTimers;
    /**
     * Generates a unique task ID.
     * Uses 16 bytes of random data encoded as hex (32 characters).
     */
    private generateTaskId;
    /**
     * Returns the stored task unless it belongs to a different session than the caller's.
     */
    private lookup;
    createTask(taskParams: CreateTaskOptions, requestId: RequestId, request: Request, sessionId?: string): Promise<Task>;
    getTask(taskId: string, sessionId?: string): Promise<Task | null>;
    storeTaskResult(taskId: string, status: 'completed' | 'failed', result: Result, sessionId?: string): Promise<void>;
    getTaskResult(taskId: string, sessionId?: string): Promise<Result>;
    updateTaskStatus(taskId: string, status: Task['status'], statusMessage?: string, sessionId?: string): Promise<void>;
    listTasks(cursor?: string, sessionId?: string): Promise<{
        tasks: Task[];
        nextCursor?: string;
    }>;
    /**
     * Cleanup all timers (useful for testing or graceful shutdown)
     */
    cleanup(): void;
    /**
     * Get all tasks of all sessions (useful for debugging)
     */
    getAllTasks(): Task[];
}
/**
 * A simple in-memory implementation of TaskMessageQueue for demonstration purposes.
 *
 * This implementation stores messages in memory, organized by task ID and optional session ID.
 * Messages are stored in FIFO queues per task.
 *
 * Note: This is not suitable for production use in distributed systems.
 * For production, consider implementing TaskMessageQueue with Redis or other distributed queues.
 *
 * @experimental
 */
export declare class InMemoryTaskMessageQueue implements TaskMessageQueue {
    private queues;
    /**
     * Generates a queue key from taskId.
     * SessionId is intentionally ignored because taskIds are globally unique
     * and the task store decides which session a task is found for.
     */
    private getQueueKey;
    /**
     * Gets or creates a queue for the given task and session.
     */
    private getQueue;
    /**
     * Adds a message to the end of the queue for a specific task.
     * Atomically checks queue size and throws if maxSize would be exceeded.
     * @param taskId The task identifier
     * @param message The message to enqueue
     * @param sessionId Optional session ID for binding the operation to a specific session
     * @param maxSize Optional maximum queue size - if specified and queue is full, throws an error
     * @throws Error if maxSize is specified and would be exceeded
     */
    enqueue(taskId: string, message: QueuedMessage, sessionId?: string, maxSize?: number): Promise<void>;
    /**
     * Removes and returns the first message from the queue for a specific task.
     * @param taskId The task identifier
     * @param sessionId Optional session ID for binding the query to a specific session
     * @returns The first message, or undefined if the queue is empty
     */
    dequeue(taskId: string, sessionId?: string): Promise<QueuedMessage | undefined>;
    /**
     * Removes and returns all messages from the queue for a specific task.
     * @param taskId The task identifier
     * @param sessionId Optional session ID for binding the query to a specific session
     * @returns Array of all messages that were in the queue
     */
    dequeueAll(taskId: string, sessionId?: string): Promise<QueuedMessage[]>;
}
//# sourceMappingURL=in-memory.d.ts.map