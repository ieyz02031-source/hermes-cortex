#!/bin/bash
# Hermes 大脑系统 - 自动自进化任务
# 运行时间: 每天晚上 9:00

cd D:\Hermes\skills\hermes-cortex
python scripts/evolve.py run >> D:\ObsidianVault\.hermes_logs/evolution.log 2>&1
python scripts/hot_cache.py >> D:\ObsidianVault\.hermes_logs/hot_cache.log 2>&1
python scripts/semantic_index.py index >> D:\ObsidianVault\.hermes_logs/index.log 2>&1
