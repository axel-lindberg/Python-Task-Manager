import java.util.ArrayList;
import java.util.List;

public class TaskManager {
    private List<Task> tasks;

    public TaskManager() {
        this.tasks = new ArrayList<>();
    }

    public void addTask(String name) {
        tasks.add(new Task(name, false));
    }

    public boolean removeTask(Task task) {
        return tasks.remove(task);
    }

    public void markTaskAsDone(Task task) {
        task.setDone(true);
    }

    public void clearTasks() {
        tasks.clear();
    }
}
