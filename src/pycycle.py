"""Find circular imports between local Python modules."""
import argparse,ast,json,sys
from pathlib import Path
def module_name(path,root):
 rel=path.relative_to(root).with_suffix("")
 parts=list(rel.parts)
 if parts[-1]=="__init__": parts.pop()
 return ".".join(parts)
def collect(root):
 root=Path(root).resolve(); files=list(root.rglob("*.py")); modules={module_name(p,root):p for p in files}; graph={m:set() for m in modules}
 for name,path in modules.items():
  try: tree=ast.parse(path.read_text(encoding="utf-8"))
  except (OSError,SyntaxError): continue
  for node in ast.walk(tree):
   target=None
   if isinstance(node,ast.Import):
    for alias in node.names:
     for mod in modules:
      if alias.name==mod or alias.name.startswith(mod+"."): graph[name].add(mod)
   elif isinstance(node,ast.ImportFrom):
    base=node.module or ""
    if node.level:
     pkg=name.split(".")[:-1]
     if node.level>1: pkg=pkg[:-(node.level-1)]
     base=".".join(pkg+[base] if base else pkg)
    for mod in modules:
     if base==mod or base.startswith(mod+".") or mod.startswith(base+".") and base:
      graph[name].add(mod)
 return graph
def cycles(graph):
 found=set()
 def walk(start,node,path):
  for nxt in graph.get(node,()):
   if nxt==start:
    ring=path[:]
    rotations=[tuple(ring[i:]+ring[:i]) for i in range(len(ring))]
    found.add(min(rotations))
   elif nxt not in path and len(path)<len(graph):
    walk(start,nxt,path+[nxt])
 for node in graph: walk(node,node,[node])
 return [list(x) for x in sorted(found)]
def main(argv=None):
 p=argparse.ArgumentParser(description="Find circular imports in a Python source tree.")
 p.add_argument("directory",nargs="?",default="."); p.add_argument("--json",action="store_true"); a=p.parse_args(argv)
 result=cycles(collect(a.directory))
 print(json.dumps(result,indent=2) if a.json else ("No import cycles found." if not result else "\n".join(" -> ".join(c+[c[0]]) for c in result)))
 return int(bool(result))
if __name__=="__main__": sys.exit(main())
