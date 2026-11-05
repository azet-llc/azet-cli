# azet 판 Pi 패치 2: 다른 도구 공용 폴더(~/.agents/skills, 프로젝트 .agents/skills)의 스킬을 읽지 않는다.
# 남는 스킬 위치 = 우리 폴더뿐: ~/.config/azet/agent/skills(에이전트 폴더) + 프로젝트 .azet/skills(piConfig.configDir).
import sys
p = f"{sys.argv[1]}/core/package-manager.ts"
s = open(p).read()
for a, b in [
    ('collectAutoSkillEntries(agentsSkillsDir, "agents")', "[]"),
    ('collectAutoSkillEntries(userAgentsSkillsDir, "agents")', "[]"),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, "w").write(s)
print("patched 2")
