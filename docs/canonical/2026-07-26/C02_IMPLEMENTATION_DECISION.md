# C02 — Decisão de implementação

A execução do Ciclo 2 será instrumentada no próprio RafPolimata por uma camada de recibo, sem alterar a semântica do compilador ou dos testes existentes.

## Decisão

Preservar `scripts/validate_runtime_truth_local.sh` como gate operacional e adicionar um wrapper responsável exclusivamente por cadeia de custódia.

## Razões

- evita duplicar os nove testes já existentes;
- mantém uma única fonte de verdade para o PASS/FAIL local;
- separa comportamento testado de coleta de evidência;
- permite execução local no Termux ou Linux e execução em GitHub Actions;
- mantém Android, instalação e aparelho explicitamente fora do escopo deste gate.

## Não será feito neste ciclo

- modificar resultados para forçar PASS;
- transformar warnings em sucesso silencioso;
- instalar dependências automaticamente;
- baixar toolchains pela rede;
- assinar APK;
- executar QEMU;
- promover claim científico ou de desempenho.

## Condição de fechamento

O C02 permanece `ACTIVE_EXECUTION_PENDING` enquanto não houver uma execução observada com receipt, logs, toolchain e hashes.