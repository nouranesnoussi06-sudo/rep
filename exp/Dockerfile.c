ARG GCC_VERSION=15
FROM gcc:${GCC_VERSION}
ARG CFLAGS="-O2"
WORKDIR /app
COPY exp/assoc_llm.c .
RUN gcc ${CFLAGS} -o assoc assoc_llm.c
CMD ["./assoc", "--repetitions=1000000", "--seed=42", "--low=-1000000", "--high=1000000"]
