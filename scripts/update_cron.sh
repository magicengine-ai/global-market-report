#!/bin/bash
#
# 全球上市公司报告 - 定时更新脚本
# 每 5 分钟执行一次
#

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
PYTHON_CMD="python3"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/cron_$(date +%Y%m%d).log"

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === 开始更新任务 ===" >> "$LOG_FILE"

# 切换到项目目录
cd "$PROJECT_DIR" || exit 1

# 运行更新脚本
$PYTHON_CMD "$SCRIPT_DIR/run.py" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# 记录结束时间
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 更新成功" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 更新失败 (退出码：$EXIT_CODE)" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

exit $EXIT_CODE
